package eajc.group.apv.mapper;

import eajc.group.apv.dto.ContributionResponseDto;
import eajc.group.apv.dto.EventRequestDto;
import eajc.group.apv.dto.EventResponseDto;
import eajc.group.apv.entity.Contribution;
import eajc.group.apv.entity.Event;
import eajc.group.apv.entity.EventType;
import eajc.group.apv.entity.User;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.List;

@Component
public class EventMapper {

    public Event toEntity(EventRequestDto dto, EventType eventType, User user){
        Event event = new Event();
        event.setName(dto.getName().trim());
        event.setMount(dto.getMount());
        event.setAmountTotal(BigDecimal.ZERO);
        event.setEventDate(dto.getEventDate());
        event.setClosure_status(dto.getClosure_status());
        event.setComment(dto.getComment().trim());
        event.setEventType(eventType);
        event.setUser(user);
        return  event;
    }

    private ContributionResponseDto toContributionDto(Contribution contribution) {
        ContributionResponseDto dto = new ContributionResponseDto();
        dto.setPublicId(contribution.getPublicId());
        dto.setAmount(contribution.getAmount());
        dto.setStatus(contribution.getStatus());
        dto.setEventId(contribution.getEvent().getId());
        dto.setContributedId(contribution.getContributed().getId());
        dto.setCreatedAt(contribution.getCreatedAt());
        return dto;
    }

    public EventResponseDto toDto(Event event){
        EventResponseDto dto = new EventResponseDto();
        dto.setId(event.getId());
        dto.setPublicId(event.getPublicId());
        dto.setName(event.getName());
        dto.setMount(event.getMount());
        dto.setAmountTotal(event.getAmountTotal());
        dto.setEventDate(event.getEventDate());
        dto.setClosure_status(event.getClosure_status());
        dto.setComment(event.getComment());
        dto.setEventTypeId(event.getEventType().getId());
        dto.setEventTypeName(event.getEventType().getName());
        dto.setUserId(event.getUser().getId());
        dto.setUserLastName(event.getUser().getProfile().getLastName());
        dto.setUserFirstName(event.getUser().getProfile().getFirstName());
        dto.setContributions(event.getContributions() == null
                ? List.of()
                : event.getContributions()
                .stream()
                .map(this::toContributionDto)
                .toList()
        );
        return  dto;
    }
}
