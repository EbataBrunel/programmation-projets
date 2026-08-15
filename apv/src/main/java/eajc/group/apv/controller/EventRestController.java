package eajc.group.apv.controller;

import eajc.group.apv.dto.*;
import eajc.group.apv.services.CaptchaService;
import eajc.group.apv.services.EventService;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/events")
public class EventRestController {

    private final EventService eventService;
    private final CaptchaService captchaService;

    public EventRestController(EventService eventService, CaptchaService captchaService) {
        this.eventService = eventService;
        this.captchaService = captchaService;
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PostMapping
    public ResponseEntity<EventResponseDto> create(
            @RequestBody EventRequestDto dto
    ){
        return ResponseEntity.ok(eventService.createEvent(dto));
    }

    // Récupérer tous les évènements
    @GetMapping
    public ResponseEntity<List<EventResponseDto>> getAll() {
        return ResponseEntity.ok(eventService.getAllEvents());
    }

    // Récupérer un évènement par id
    @GetMapping("/{publicId}")
    public ResponseEntity<EventResponseDto> getOne(
            @PathVariable UUID publicId
            ) {
        return ResponseEntity.ok(eventService.getEventByPublicId(publicId));
    }

    // Récupérer un évènement par id
    @GetMapping("/id/{id}")
    public ResponseEntity<EventResponseDto> getEventById(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(eventService.getEventById(id));
    }

    @GetMapping("/count/event")
    public ResponseEntity<List<EventTypeCountDto>> getCountEventsByEventType() {
        return ResponseEntity.ok(eventService.countEventsByEventType());
    }

    @GetMapping("events/{eventTypeId}")
    public ResponseEntity<List<EventResponseDto>> findEventByEventTypeId(
            @PathVariable Long eventTypeId
    ) {

        return ResponseEntity.ok(eventService.findByEventTypeId(eventTypeId));
    }

    @PreAuthorize("hasRole('SUPADMIN')")
    // Modifier un évènement
    @PatchMapping("/update-closure-status/{publicId}")
    public ResponseEntity<?> updateClosureStatus(
            @PathVariable UUID publicId,
            @RequestBody ClosureRequest request
    ) {

        boolean captchaValid = captchaService.verifyCaptcha(request.getCaptchaToken());


        if(!captchaValid){

            return ResponseEntity
                    .badRequest()
                    .body("Captcha invalide");

        }

        return ResponseEntity.ok(eventService.updateClosureStatusEvent(publicId));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Modifier un évènement
    @PatchMapping("/{publicId}")
    public ResponseEntity<EventResponseDto> update(
            @PathVariable UUID publicId,
            @RequestBody EventRequestDto dto
    ) {
        return ResponseEntity.ok(eventService.updateEvent(publicId, dto));
    }

    @GetMapping("/statistics/by-year")
    public ResponseEntity<List<EventCountByYearDto>> countEventsByYear() {
        return ResponseEntity.ok(
                eventService.countEventsByYear()
        );
    }

    @GetMapping("/month")
    public ResponseEntity<List<EventResponseDto>> getEventsByMonth(
            @RequestParam int year,
            @RequestParam int month
    ) {
        return ResponseEntity.ok(
                eventService.getEventsByMonth(year, month)
        );
    }

    @GetMapping("/year")
    public ResponseEntity<List<EventResponseDto>> getEventsByYear(
            @RequestParam int year
    ) {
        return ResponseEntity.ok(
                eventService.getEventsByYear(year)
        );
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer un évènement
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        eventService.deleteEvent(publicId);
        return ResponseEntity.noContent().build();
    }
}
