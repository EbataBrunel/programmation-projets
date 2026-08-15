package eajc.group.apv.controller;

import eajc.group.apv.dto.RegulationRequestDto;
import eajc.group.apv.dto.RegulationResponseDto;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.services.CustomUserDetails;
import eajc.group.apv.services.RegulationService;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/regulations")
public class RegulationRestController {
    private final RegulationService regulationService;

    public RegulationRestController(RegulationService regulationService) {
        this.regulationService = regulationService;
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<RegulationResponseDto> create(
            @RequestPart("data") RegulationRequestDto dto,
            Authentication authentication
    ){
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new ResourceNotFoundException("Utilisateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();

        return ResponseEntity.ok(regulationService.createRegulation(dto, user.getUser().getId()));
    }

    // Récupérer tous les règlements
    @GetMapping
    public ResponseEntity<List<RegulationResponseDto>> getAll() {
        return ResponseEntity.ok(regulationService.getAllRegulations());
    }

    // Récupérer un règlement par id
    @GetMapping("/{publicId}")
    public ResponseEntity<RegulationResponseDto> getOne(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(regulationService.getRegulationByPublicId(publicId));
    }

    // Modifier un règlement
    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PatchMapping(value="/{publicId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<RegulationResponseDto> update(
            @PathVariable UUID publicId,
            @RequestPart("data") RegulationRequestDto dto,
            Authentication authentication
    ) {
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new ResourceNotFoundException("Utilisateur non authentifié");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();

        return ResponseEntity.ok(regulationService.updateRegulation(publicId, dto, user.getUser().getId()));
    }

    // Supprimer un règlement
    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        regulationService.deleteRegulation(publicId);
        return ResponseEntity.noContent().build();
    }
}
