package eajc.group.apv.services;

import com.lowagie.text.*;
import com.lowagie.text.Font;
import com.lowagie.text.Rectangle;
import com.lowagie.text.pdf.PdfPCell;
import com.lowagie.text.pdf.PdfPTable;
import com.lowagie.text.pdf.PdfWriter;
import eajc.group.apv.dto.ContributionPdfDto;
import eajc.group.apv.entity.Setting;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.repository.SettingRepository;
import org.springframework.stereotype.Service;

import java.awt.*;
import com.lowagie.text.Image;
import java.io.ByteArrayOutputStream;
import java.math.BigDecimal;
import java.net.URL;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
public class ContributionPdfServiceImpl implements ContributionPdfService{

    private final SettingRepository settingRepository;

    public ContributionPdfServiceImpl(SettingRepository settingRepository) {
        this.settingRepository = settingRepository;
    }

    @Override
    public byte[] generate(List<ContributionPdfDto> contributions) throws Exception {

        ByteArrayOutputStream out = new ByteArrayOutputStream();

        Document document = new Document(PageSize.A4.rotate());

        PdfWriter.getInstance(document, out);

        document.open();


        /*
         * ==============================
         * Récupération configuration
         * ==============================
         */

        Setting setting = settingRepository
                .findFirstByOrderByIdAsc()
                .orElseThrow(() ->
                        new ResourceNotFoundException("Paramètres introuvables")
                );


        /*
         * ==============================
         * Header : Logo + informations
         * ==============================
         */

        PdfPTable header = createHeader(setting);

        document.add(header);

        document.add(new Paragraph(" "));


        /*
         * ==============================
         * Titre du document
         * ==============================
         */

        Font titleFont = new Font(
                Font.HELVETICA,
                16,
                Font.BOLD
        );


        Paragraph title = new Paragraph(
                "LISTE DES CONTRIBUTIONS",
                titleFont
        );

        title.setAlignment(Element.ALIGN_CENTER);

        document.add(title);


        document.add(new Paragraph(" "));


        /*
         * ==============================
         * Tableau des contributions
         * ==============================
         */


        PdfPTable table = new PdfPTable(6);

        table.setWidthPercentage(100);

        table.setWidths(new float[]{
                3,3,3,2,2,3
        });


        addHeader(table,"Contributeur");
        addHeader(table,"Bénéficiaire");
        addHeader(table,"Evènement");
        addHeader(table,"Montant");
        addHeader(table,"Statut");
        addHeader(table,"Date");


        BigDecimal total = BigDecimal.ZERO;


        for(ContributionPdfDto c : contributions){


            table.addCell(c.getContributedName());

            table.addCell(c.getBeneficiaryName());

            table.addCell(c.getEventName());


            table.addCell(
                    c.getMontant()
                            .toString()
                            + " "
                            + setting.getCurrency()
            );


            table.addCell(c.getStatut());


            table.addCell(
                    c.getDate()
                            .format(
                                    DateTimeFormatter.ofPattern(
                                            "dd/MM/yyyy"
                                    )
                            )
            );


            total = total.add(c.getMontant());

        }


        document.add(table);


        /*
         * ==============================
         * Total
         * ==============================
         */

        document.add(new Paragraph(" "));


        Paragraph totalParagraph =
                new Paragraph(
                        "Montant total : "
                                + total
                                + " "
                                + setting.getCurrency()
                );


        totalParagraph.setAlignment(
                Element.ALIGN_RIGHT
        );


        document.add(totalParagraph);


        /*
         * ==============================
         * Fermeture
         * ==============================
         */

        document.close();


        return out.toByteArray();
    }

    public PdfPTable createHeader(Setting setting) throws Exception {


        PdfPTable header = new PdfPTable(2);

        header.setWidthPercentage(100);

        header.setWidths(
                new float[]{1,4}
        );


        header.getDefaultCell()
                .setBorder(Rectangle.NO_BORDER);



        /*
         * Logo
         */

        String url =
                "http://127.0.0.1:8080/uploads/"
                        + setting.getLogo();


        Image logo =
                Image.getInstance(
                        new URL(url)
                );


        logo.scaleToFit(
                setting.getWidth(),
                setting.getHeight()
        );



        PdfPCell logoCell =
                new PdfPCell();


        logoCell.setBorder(
                Rectangle.NO_BORDER
        );


        logoCell.addElement(logo);



        /*
         * Informations
         */


        PdfPCell infoCell =
                new PdfPCell();


        infoCell.setBorder(
                Rectangle.NO_BORDER
        );


        Font appFont =
                new Font(
                        Font.HELVETICA,
                        18,
                        Font.BOLD
                );


        Font infoFont =
                new Font(
                        Font.HELVETICA,
                        10
                );



        infoCell.addElement(
                new Paragraph(
                        setting.getNameApp(),
                        appFont
                )
        );


        infoCell.addElement(
                new Paragraph(
                        "Adresse : "
                                + setting.getAddress(),
                        infoFont
                )
        );


        infoCell.addElement(
                new Paragraph(
                        "Email : "
                                + setting.getEmail(),
                        infoFont
                )
        );


        infoCell.addElement(
                new Paragraph(
                        "Téléphone : "
                                + setting.getPhone(),
                        infoFont
                )
        );


        infoCell.addElement(
                new Paragraph(
                        "Version : "
                                + setting.getVersion(),
                        infoFont
                )
        );



        header.addCell(logoCell);

        header.addCell(infoCell);



        return header;
    }

    @Override
    public void addHeader(PdfPTable table, String text) {
        PdfPCell cell = new PdfPCell(new Phrase(text));

        cell.setBackgroundColor(Color.LIGHT_GRAY);

        cell.setHorizontalAlignment(Element.ALIGN_CENTER);

        table.addCell(cell);
    }
}
