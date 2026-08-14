package eajc.group.apv.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

public class ContributionPdfDto {

    private UUID publicId;

    private String contributedName;

    private String eventName;

    private String beneficiaryName;

    private BigDecimal montant;

    private String statut;

    private LocalDateTime date;

    public ContributionPdfDto(){}

    public ContributionPdfDto(UUID publicId, String contributedName, String eventName, String beneficiaryName, BigDecimal montant, String statut, LocalDateTime date) {
        this.publicId = publicId;
        this.contributedName = contributedName;
        this.eventName = eventName;
        this.beneficiaryName = beneficiaryName;
        this.montant = montant;
        this.statut = statut;
        this.date = date;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
    }

    public String getContributedName() {
        return contributedName;
    }

    public void setContributedName(String contributedName) {
        this.contributedName = contributedName;
    }

    public String getEventName() {
        return eventName;
    }

    public void setEventName(String eventName) {
        this.eventName = eventName;
    }

    public String getBeneficiaryName() {
        return beneficiaryName;
    }

    public void setBeneficiaryName(String beneficiaryName) {
        this.beneficiaryName = beneficiaryName;
    }

    public BigDecimal getMontant() {
        return montant;
    }

    public void setMontant(BigDecimal montant) {
        this.montant = montant;
    }

    public String getStatut() {
        return statut;
    }

    public void setStatut(String statut) {
        this.statut = statut;
    }

    public LocalDateTime getDate() {
        return date;
    }

    public void setDate(LocalDateTime date) {
        this.date = date;
    }
}
