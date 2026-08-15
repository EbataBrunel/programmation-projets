package eajc.group.apv.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

public class DonationParticipantResponseDto {

    private Long id;

    private UUID publicId;

    private String name;

    private String itemType;

    private String description;

    private BigDecimal amount; // uniquement si itemType == MONEY

    private LocalDateTime participationDate;

    private Long donationId;

    private String donationTitle;

    private Long userId;

    private String userLastName;

    private String userFirstName;

    public DonationParticipantResponseDto(){}

    public DonationParticipantResponseDto(Long id, UUID publicId, String name, String itemType, String description, BigDecimal amount, LocalDateTime participationDate, Long donationId, String donationTitle, Long userId, String userLastName, String userFirstName) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.itemType = itemType;
        this.description = description;
        this.amount = amount;
        this.participationDate = participationDate;
        this.donationId = donationId;
        this.donationTitle = donationTitle;
        this.userId = userId;
        this.userLastName = userLastName;
        this.userFirstName = userFirstName;
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

    public String getItemType() {
        return itemType;
    }

    public void setItemType(String itemType) {
        this.itemType = itemType;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public BigDecimal getAmount() {
        return amount;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public LocalDateTime getParticipationDate() {
        return participationDate;
    }

    public void setParticipationDate(LocalDateTime participationDate) {
        this.participationDate = participationDate;
    }

    public Long getDonationId() {
        return donationId;
    }

    public void setDonationId(Long donationId) {
        this.donationId = donationId;
    }

    public String getDonationTitle() {
        return donationTitle;
    }

    public void setDonationTitle(String donationTitle) {
        this.donationTitle = donationTitle;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getUserLastName() {
        return userLastName;
    }

    public void setUserLastName(String userLastName) {
        this.userLastName = userLastName;
    }

    public String getUserFirstName() {
        return userFirstName;
    }

    public void setUserFirstName(String userFirstName) {
        this.userFirstName = userFirstName;
    }
}
