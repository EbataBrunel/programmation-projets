package eajc.group.apv.controller;

import eajc.group.apv.dto.*;
import eajc.group.apv.services.ContributionService;
import eajc.group.apv.services.CustomUserDetails;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/contributions")
public class ContributionController {
    private final ContributionService contributionService;

    public ContributionController(ContributionService contributionService) {
        this.contributionService = contributionService;
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<ContributionResponseDto> create(
            @RequestPart("data") ContributionRequestDto dto,
            Authentication authentication
    ){
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Utilisateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();
        return ResponseEntity.ok(contributionService.createContribution(dto, user.getUser().getId()));
    }

    // Récupérer tous les contributions
    @GetMapping
    public ResponseEntity<List<ContributionResponseDto>> getAll() {
        return ResponseEntity.ok(contributionService.getAllContributions());
    }

    // Récupérer une contribution par publicId
    @GetMapping("/{publicId}")
    public ResponseEntity<ContributionResponseDto> getOne(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(contributionService.getContributionByPublicId(publicId));
    }

    // Récupérer toutes les contributions d'un évènement
    @GetMapping("/event/{publicId}")
    public ResponseEntity<List<ContributionResponseDto>> getContributionByEvent(
            @PathVariable UUID publicId
    ) {

        return ResponseEntity.ok(contributionService.getContributionsByEvent(publicId));
    }

    // Récupérer toutes les contributions d'un évènement
    @GetMapping("/contributed/{publicId}")
    public ResponseEntity<List<ContributionResponseDto>> getContributionByContributed(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(contributionService.getContributionsByContributed(publicId));
    }

    @GetMapping("/event-types/contribution-count")
    public ResponseEntity<List<EventTypeContributionCountDto>> getCountEventByEventTypeWithContribution() {
        return ResponseEntity.ok(contributionService.countEventByEventTypeWithContribution());
    }

    @GetMapping("/count-contributions-by-event/{eventTypePublicId}")
    public ResponseEntity<List<ContributionsByEventCountDto>> getCountContributionsByEventAndEventType(
            @PathVariable UUID eventTypePublicId
    ) {
        return ResponseEntity.ok(contributionService.countContributionsByEventAndEventType(eventTypePublicId));
    }

    @GetMapping("/exports/pdf")
    public ResponseEntity<byte[]> exportPdf() throws Exception {

        byte[] pdf = contributionService.exportPdf();

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=contributions.pdf")
                .contentType(MediaType.APPLICATION_PDF)
                .body(pdf);

    }

    @GetMapping("/event/{eventId}/total")
    public ResponseEntity<BigDecimal> getEventTotal(
            @PathVariable Long eventId
    ) {
        BigDecimal total = contributionService.calculateEventTotal(eventId);

        return ResponseEntity.ok(total);
    }

    @GetMapping("/grouped-by-contributed")
    public ResponseEntity<List<ContributedCountDTO>> getCountContributionsByContributed() {

        return ResponseEntity.ok(
                contributionService.countContributionsByContributed()
        );
    }

    @GetMapping("/count-contributions-by-eventtype")
    public List<ContributionCountByEventTypeDTO> countContributionsByEventType() {
        return contributionService.countContributionsByEventType();
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Modifier un évènement
    @PatchMapping(value="/{publicId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<ContributionResponseDto> update(
            @PathVariable UUID publicId,
            @RequestPart("data") ContributionRequestDto dto,
            Authentication authentication
    ) {
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("Utilisateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();
        return ResponseEntity.ok(contributionService.updateContribution(publicId, dto, user.getUser().getId()));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer un évènement
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        contributionService.deleteContribution(publicId);
        return ResponseEntity.noContent().build();
    }
}
