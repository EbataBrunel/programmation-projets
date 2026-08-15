package eajc.group.apv.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

public class ContributionResponseDto {

    private UUID publicId;

    private Long contributedId;

    private Long eventId;

    private String eventName;

    private Long userId;

    private String userLastName;

    private String userFirstName;

    private BigDecimal amount;

    private Boolean status;

    private LocalDateTime createdAt;

    public ContributionResponseDto(){}

    public ContributionResponseDto(UUID publicId, Long contributedId, Long eventId, String eventName, Long userId, String userLastName, String userFirstName, BigDecimal amount, Boolean status, LocalDateTime createdAt) {
        this.publicId = publicId;
        this.contributedId = contributedId;
        this.eventId = eventId;
        this.eventName = eventName;
        this.userId = userId;
        this.userLastName = userLastName;
        this.userFirstName = userFirstName;
        this.amount = amount;
        this.status = status;
        this.createdAt = createdAt;
    }

    public UUID getPublicId() {
        return publicId;
    }

    public void setPublicId(UUID publicId) {
        this.publicId = publicId;
    }

    public Long getContributedId() {
        return contributedId;
    }

    public void setContributedId(Long contributedId) {
        this.contributedId = contributedId;
    }

    public Long getEventId() {
        return eventId;
    }

    public void setEventId(Long eventId) {
        this.eventId = eventId;
    }

    public String getEventName() {
        return eventName;
    }

    public void setEventName(String eventName) {
        this.eventName = eventName;
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

    public BigDecimal getAmount() {
        return amount;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public Boolean getStatus() {
        return status;
    }

    public void setStatus(Boolean status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
