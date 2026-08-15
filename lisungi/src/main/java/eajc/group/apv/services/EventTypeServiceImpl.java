package eajc.group.apv.services;

import eajc.group.apv.dto.EventTypeRequestDto;
import eajc.group.apv.dto.EventTypeResponseDto;
import eajc.group.apv.entity.EventType;
import eajc.group.apv.exception.BadRequestException;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.EventTypeMapper;
import eajc.group.apv.repository.EventTypeRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class EventTypeServiceImpl implements EventTypeService {

    private final EventTypeRepository eventTypeRepository;
    private final EventTypeMapper eventTypeMapper;

    public EventTypeServiceImpl(
            EventTypeRepository eventTypeRepository,
            EventTypeMapper eventTypeMapper
    ) {
        this.eventTypeRepository = eventTypeRepository;
        this.eventTypeMapper = eventTypeMapper;
    }

    @Override
    public EventTypeResponseDto createEventType(EventTypeRequestDto dto) {
        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom est obligatoire.");
        }

        if (eventTypeRepository.existsByNameIgnoreCase(dto.getName().trim())) {
            throw new BadRequestException("Ce nom existe déjà.");
        }

        EventType eventType = eventTypeMapper.toEntity(dto);
        EventType eventTypeSave = eventTypeRepository.save(eventType);
        return eventTypeMapper.toDto(eventTypeSave);
    }

    @Override
    public List<EventTypeResponseDto> getAllEventTypes() {
        return eventTypeRepository.findAll()
                .stream()
                .map(eventTypeMapper::toDto)
                .toList();
    }

    @Override
    public EventTypeResponseDto getEventTypeByPublicId(UUID publicId) {
        EventType eventType = eventTypeRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Event not found"));
        return eventTypeMapper.toDto(eventType);
    }

    @Override
    public EventTypeResponseDto updateEventType(UUID publicId, EventTypeRequestDto dto) {
        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new BadRequestException("Le nom est obligatoire.");
        }

        EventType eventType = eventTypeRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Type d'évènement introuvable"));

        if (eventTypeRepository.existsByNameIgnoreCaseAndPublicIdNot(
                dto.getName().trim(),
                eventType.getPublicId()
        )) {
            throw new BadRequestException("Ce nom existe déjà.");
        }

        eventType.setName(dto.getName().trim());
        return eventTypeMapper.toDto(eventTypeRepository.save(eventType));
    }

    @Override
    public void deleteEventType(UUID publicId) {
        EventType eventType = eventTypeRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Type d'évènement introuvable"));
        eventTypeRepository.delete(eventType);
    }
}