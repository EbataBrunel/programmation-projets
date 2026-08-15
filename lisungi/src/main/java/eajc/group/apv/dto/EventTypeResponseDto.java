package eajc.group.apv.dto;


import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class EventTypeResponseDto {
    public Long id;
    private UUID publicId;
    private String name;
    private List<EventResponseDto> events = new ArrayList<>();

    public EventTypeResponseDto(){}

    public EventTypeResponseDto(Long id, UUID publicId, String name, List<EventResponseDto> events) {
        this.id = id;
        this.publicId = publicId;
        this.name = name;
        this.events = events;
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

    public List<EventResponseDto> getEvents() {
        return events;
    }

    public void setEvents(List<EventResponseDto> events) {
        this.events = events;
    }
}
