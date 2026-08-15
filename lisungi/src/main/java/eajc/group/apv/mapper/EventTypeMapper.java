package eajc.group.apv.mapper;

import eajc.group.apv.dto.EventResponseDto;
import eajc.group.apv.dto.EventTypeRequestDto;
import eajc.group.apv.dto.EventTypeResponseDto;
import eajc.group.apv.entity.Event;
import eajc.group.apv.entity.EventType;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class EventTypeMapper {

    ContributionMapper contributionMapper = new ContributionMapper();

    public EventTypeMapper(ContributionMapper contributionMapper) {
        this.contributionMapper = contributionMapper;
    }

    public EventType toEntity(EventTypeRequestDto dto){
        EventType eventType = new EventType();
        eventType.setName(dto.getName().trim());
        return  eventType;
    }

    private EventResponseDto toEventDto(Event event) {
        EventResponseDto dto = new EventResponseDto();
        dto.setId(event.getId());
        dto.setPublicId(event.getPublicId());
        dto.setName(event.getName());;
        dto.setMount(event.getMount());
        dto.setEventDate(event.getEventDate());
        dto.setComment(event.getComment());
        dto.setUserId(event.getUser().getId());
        dto.setClosure_status(event.getClosure_status());
        dto.setContributions(event.getContributions() == null
                ? List.of()
                : event.getContributions()
                .stream()
                .map(contributionMapper::toDto)
                .toList()
        );
        return dto;
    }

    public EventTypeResponseDto toDto(EventType eventType){
        EventTypeResponseDto dto = new EventTypeResponseDto();
        dto.setId(eventType.getId());
        dto.setPublicId(eventType.getPublicId());
        dto.setName(eventType.getName());
        dto.setEvents(eventType.getEvents() == null
                ? List.of()
                : eventType.getEvents()
                .stream()
                .map(this::toEventDto)
                .toList()
        );
        return  dto;
    }
}
