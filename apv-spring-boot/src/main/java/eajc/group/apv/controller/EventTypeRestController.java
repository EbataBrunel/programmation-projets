package eajc.group.apv.controller;

import eajc.group.apv.dto.EventTypeRequestDto;
import eajc.group.apv.dto.EventTypeResponseDto;
import eajc.group.apv.services.EventTypeService;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/event-types")
public class EventTypeRestController {

    private final EventTypeService eventTypeService;

    public EventTypeRestController(EventTypeService eventTypeService) {
        this.eventTypeService = eventTypeService;
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<EventTypeResponseDto> create(
            @RequestPart("data") EventTypeRequestDto dto
    ){
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(eventTypeService.createEventType(dto));
    }

    // Récupérer tous les Types d'évènements
    @GetMapping
    public ResponseEntity<List<EventTypeResponseDto>> getAll() {
        return ResponseEntity.ok(eventTypeService.getAllEventTypes());
    }

    // Récupérer un Type d'évènement par id
    @GetMapping("/{publicId}")
    public ResponseEntity<EventTypeResponseDto> getOne(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(eventTypeService.getEventTypeByPublicId(publicId));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Modifier un Type d'évènement
    @PatchMapping(value="/{publicId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<EventTypeResponseDto> update(
            @PathVariable UUID publicId,
            @RequestPart("data") EventTypeRequestDto dto
    ) {
        return ResponseEntity.ok(eventTypeService.updateEventType(publicId, dto));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer un Type évènement
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        eventTypeService.deleteEventType(publicId);
        return ResponseEntity.noContent().build();
    }
}
