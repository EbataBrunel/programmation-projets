package eajc.group.apv.dto;

import java.util.UUID;

public class BeneficiaryDonationParticipantCountDto {
    private Long id;
    private UUID publicId;
    private String name;
    private Long totalDonations;

    public BeneficiaryDonationParticipantCountDto(Long id, UUID publicId, String name, Long totalDonations) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.totalDonations = totalDonations;
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

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Long getTotalDonations() {
        return totalDonations;
    }

    public void setTotalDonations(Long totalDonations) {
        this.totalDonations = totalDonations;
    }
}
