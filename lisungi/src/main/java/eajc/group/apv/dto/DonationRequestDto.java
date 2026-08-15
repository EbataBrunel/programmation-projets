package eajc.group.apv.dto;

import eajc.group.apv.entity.Beneficiary;

import java.math.BigDecimal;
import java.time.LocalDate;

public class DonationRequestDto {

    private String title;

    private String description;

    private LocalDate dateDonation;

    private Long beneficiaryId;

    private String photo;

    public DonationRequestDto(){}

    public DonationRequestDto(String title, LocalDate dateDonation, String description, Long beneficiaryId, String photo) {
        this.title = title;
        this.dateDonation = dateDonation;
        this.description = description;
        this.beneficiaryId = beneficiaryId;
        this.photo = photo;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public LocalDate getDateDonation() {
        return dateDonation;
    }

    public void setDateDonation(LocalDate dateDonation) {
        this.dateDonation = dateDonation;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Long getBeneficiaryId() {
        return beneficiaryId;
    }

    public void setBeneficiaryId(Long beneficiaryId) {
        this.beneficiaryId = beneficiaryId;
    }

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }
}
