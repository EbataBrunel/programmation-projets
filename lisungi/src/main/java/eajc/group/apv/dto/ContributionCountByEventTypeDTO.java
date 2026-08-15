package eajc.group.apv.dto;

import java.util.UUID;

public class ContributionCountByEventTypeDTO {

    private Long eventTypeId;
    private UUID eventTypePublicId;
    private String eventTypeName;
    private Long contributionCount;


    public ContributionCountByEventTypeDTO(Long eventTypeId, UUID eventTypePublicId, String eventTypeName, Long contributionCount) {
        this.eventTypeId = eventTypeId;
        this.eventTypePublicId = eventTypePublicId;
        this.eventTypeName = eventTypeName;
        this.contributionCount = contributionCount;
    }

    public Long getEventTypeId() {
        return eventTypeId;
    }

    public void setEventTypeId(Long eventTypeId) {
        this.eventTypeId = eventTypeId;
    }

    public UUID getEventTypePublicId() {
        return eventTypePublicId;
    }

    public void setEventTypePublicId(UUID eventTypePublicId) {
        this.eventTypePublicId = eventTypePublicId;
    }

    public String getEventTypeName() {
        return eventTypeName;
    }

    public void setEventTypeName(String eventTypeName) {
        this.eventTypeName = eventTypeName;
    }

    public Long getContributionCount() {
        return contributionCount;
    }

    public void setContributionCount(Long contributionCount) {
        this.contributionCount = contributionCount;
    }
}
