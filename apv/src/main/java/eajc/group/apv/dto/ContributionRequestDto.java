package eajc.group.apv.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class ContributionRequestDto {

    private Long contributedId;

    private Long eventId;

    private Long userId;

    @NotNull(message = "Le montant est obligatoire")
    @DecimalMin(value = "0.0", inclusive = true, message = "Le montant doit être positif")
    private BigDecimal amount;

    private Boolean status;

    public ContributionRequestDto(){}

    public ContributionRequestDto(Long contributedId, Long eventId, Long userId, BigDecimal amount, Boolean status) {
        this.contributedId = contributedId;
        this.eventId = eventId;
        this.userId = userId;
        this.amount = amount;
        this.status = status;
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

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
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
}
