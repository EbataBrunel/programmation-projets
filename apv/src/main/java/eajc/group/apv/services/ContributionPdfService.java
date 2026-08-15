package eajc.group.apv.services;

import com.lowagie.text.pdf.PdfPTable;
import eajc.group.apv.dto.ContributionPdfDto;
import eajc.group.apv.entity.Setting;

import java.util.List;

public interface ContributionPdfService {

    public byte[] generate(List<ContributionPdfDto> contributions) throws Exception;
    public PdfPTable createHeader(Setting setting) throws Exception;
    public void addHeader(PdfPTable table, String text);
}
