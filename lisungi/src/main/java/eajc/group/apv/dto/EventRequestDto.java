package eajc.group.apv.dto;


import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;
import java.time.LocalDate;

public class EventRequestDto {

    @NotBlank(message = "Le nom est obligatoire")
    private String name;

    @NotNull(message = "Le montant est obligatoire")
    @DecimalMin(value = "0.0", inclusive = true, message = "Le montant doit être positif")
    private BigDecimal mount;

    private BigDecimal amountTotal;

    @NotNull(message = "La date est obligatoire")
    private LocalDate eventDate;

    private Boolean closure_status;

    private String comment;

    private Long eventTypeId;

    private Long userId;

    public EventRequestDto(){}

    public EventRequestDto(String name, BigDecimal mount, BigDecimal amountTotal, LocalDate eventDate, Boolean closure_status, String comment, Long eventTypeId, Long userId) {
        this.name = name;
        this.mount = mount;
        this.amountTotal = amountTotal;
        this.eventDate = eventDate;
        this.closure_status = closure_status;
        this.comment = comment;
        this.eventTypeId = eventTypeId;
        this.userId = userId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public BigDecimal getMount() {
        return mount;
    }

    public void setMount(BigDecimal mount) {
        this.mount = mount;
    }

    public BigDecimal getAmountTotal() {
        return amountTotal;
    }

    public void setAmountTotal(BigDecimal amountTotal) {
        this.amountTotal = amountTotal;
    }

    public LocalDate getEventDate() {
        return eventDate;
    }

    public void setEventDate(LocalDate eventDate) {
        this.eventDate = eventDate;
    }

    public Boolean getClosure_status() {
        return closure_status;
    }

    public void setClosure_status(Boolean closure_status) {
        this.closure_status = closure_status;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public Long getEventTypeId() {
        return eventTypeId;
    }

    public void setEventTypeId(Long eventTypeId) {
        this.eventTypeId = eventTypeId;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }
}
