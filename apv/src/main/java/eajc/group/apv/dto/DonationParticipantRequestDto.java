package eajc.group.apv.dto;

import eajc.group.apv.enums.DonationItemType;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class DonationParticipantRequestDto {

    private String name;

    private DonationItemType itemType;

    private String description;

    private BigDecimal amount; // uniquement si itemType == MONEY

    private LocalDateTime participationDate;

    private Long donationId;

    private Long userId;

    public DonationParticipantRequestDto(){}

    public DonationParticipantRequestDto(String name, DonationItemType itemType, String description, BigDecimal amount, LocalDateTime participationDate, Long donationId, Long userId) {
        this.name = name;
        this.itemType = itemType;
        this.description = description;
        this.amount = amount;
        this.participationDate = participationDate;
        this.donationId = donationId;
        this.userId = userId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public DonationItemType getItemType() {
        return itemType;
    }

    public void setItemType(DonationItemType itemType) {
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

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }
}
