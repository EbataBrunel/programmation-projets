package eajc.group.apv.dto;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public class DonationResponseDto {

    private Long id;

    private UUID publicId;

    private String title;

    private LocalDate dateDonation;

    private Boolean closure_status;

    private String description;

    private Long beneficiaryId;

    private String beneficiaryName;

    private String photo;

    private Boolean publicStatus;

    private List<DonationParticipantResponseDto> participants;

    public DonationResponseDto(){}

    public DonationResponseDto(Long id, UUID publicId, String title, LocalDate dateDonation, Boolean closure_status, String description, Long beneficiaryId, String beneficiaryName, String photo, Boolean publicStatus, List<DonationParticipantResponseDto> participants) {
        this.id = id;
        this.publicId = publicId;
        this.title = title;
        this.dateDonation = dateDonation;
        this.closure_status = closure_status;
        this.description = description;
        this.beneficiaryId = beneficiaryId;
        this.beneficiaryName = beneficiaryName;
        this.photo = photo;
        this.publicStatus = publicStatus;
        this.participants = participants;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
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

    public Boolean getClosure_status() {
        return closure_status;
    }

    public void setClosure_status(Boolean closure_status) {
        this.closure_status = closure_status;
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

    public String getBeneficiaryName() {
        return beneficiaryName;
    }

    public void setBeneficiaryName(String beneficiaryName) {
        this.beneficiaryName = beneficiaryName;
    }

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }

    public Boolean getPublicStatus() {
        return publicStatus;
    }

    public void setPublicStatus(Boolean publicStatus) {
        this.publicStatus = publicStatus;
    }

    public List<DonationParticipantResponseDto> getParticipants() {
        return participants;
    }

    public void setParticipants(List<DonationParticipantResponseDto> participants) {
        this.participants = participants;
    }
}
