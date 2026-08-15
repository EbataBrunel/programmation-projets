package eajc.group.apv.dto;

import java.util.UUID;

public class ParticipantsByDonationCountDto {

    private Long id;
    private UUID publicId;
    private String title;
    private Boolean closure_status;
    private Long totalParrticipant;

    public ParticipantsByDonationCountDto(){}

    public ParticipantsByDonationCountDto(Long id, UUID publicId, String title, Boolean closure_status, Long totalParrticipant) {
        this.id = id;
        this.publicId = publicId;
        this.title = title;
        this.closure_status = closure_status;
        this.totalParrticipant = totalParrticipant;
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

    public Boolean getClosure_status() {
        return closure_status;
    }

    public void setClosure_status(Boolean closure_status) {
        this.closure_status = closure_status;
    }

    public Long getTotalParrticipant() {
        return totalParrticipant;
    }

    public void setTotalParrticipant(Long totalParrticipant) {
        this.totalParrticipant = totalParrticipant;
    }
}
