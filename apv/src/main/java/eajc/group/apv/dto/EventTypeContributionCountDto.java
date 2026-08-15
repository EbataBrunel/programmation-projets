package eajc.group.apv.dto;

import java.util.UUID;

public class EventTypeContributionCountDto {
    private Long id;
    private UUID publicId;
    private String name;
    private Long totalEvents;

    public EventTypeContributionCountDto(Long id, UUID publicId, String name, Long totalEvents) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.totalEvents = totalEvents;
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

    public Long getTotalEvents() {
        return totalEvents;
    }

    public void setTotalEvents(Long totalEvents) {
        this.totalEvents = totalEvents;
    }
}
