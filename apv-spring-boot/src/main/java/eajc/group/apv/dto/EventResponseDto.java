package eajc.group.apv.dto;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public class EventResponseDto {

    private Long id;

    private UUID publicId;

    private String name;

    private BigDecimal mount;

    private BigDecimal amountTotal;

    private LocalDate eventDate;

    private Boolean closure_status;

    private String comment;

    private Long eventTypeId;

    private String eventTypeName;

    private Long userId;

    private String userLastName;

    private String userFirstName;

    private List<ContributionResponseDto> contributions;

    public EventResponseDto(){}

    public EventResponseDto(Long id, UUID publicId, String name, BigDecimal mount, BigDecimal amountTotal, Boolean closure_status, LocalDate eventDate, String comment, Long eventTypeId, String eventTypeName, Long userId, String userLastName, String userFirstName, List<ContributionResponseDto> contributions) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.mount = mount;
        this.amountTotal = amountTotal;
        this.closure_status = closure_status;
        this.eventDate = eventDate;
        this.comment = comment;
        this.eventTypeId = eventTypeId;
        this.eventTypeName = eventTypeName;
        this.userId = userId;
        this.userLastName = userLastName;
        this.userFirstName = userFirstName;
        this.contributions = contributions;
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

    public BigDecimal getMount() {
        return mount;
    }

    public void setMount(BigDecimal mount) {
        this.mount = mount;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
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

    public String getEventTypeName() {
        return eventTypeName;
    }

    public void setEventTypeName(String eventTypeName) {
        this.eventTypeName = eventTypeName;
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

    public List<ContributionResponseDto> getContributions() {
        return contributions;
    }

    public void setContributions(List<ContributionResponseDto> contributions) {
        this.contributions = contributions;
    }
}
