package eajc.group.apv.controller;

import eajc.group.apv.dto.*;
import eajc.group.apv.services.*;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/settings")
public class SettingRestController {

    private final SettingService settingService;

    public SettingRestController(SettingService settingService) {
        this.settingService = settingService;
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PostMapping
    public SettingResponseDto create(
            @RequestBody SettingRequestDto dto,
            @RequestParam(value = "logo", required = false) MultipartFile logoFile
    ) throws IOException {

        return settingService.createSetting(dto, logoFile);
    }

    // Récupérer toutes les sous paramètre
    @GetMapping
    public ResponseEntity<List<SettingResponseDto>> getAll() {
        return ResponseEntity.ok(settingService.getAllSetting());
    }

    // Récupérer un paramètre par publicId
    @GetMapping("/{publicId}")
    public ResponseEntity<SettingResponseDto> getOne(
            @PathVariable UUID publicId
            ) {
        return ResponseEntity.ok(settingService.getSettingByPublicId(publicId));
    }

    // Récupérer le dernier paramètre
    @GetMapping("/latest")
    public ResponseEntity<SettingResponseDto> getLast() {
        return ResponseEntity.ok(settingService.getLastSetting());
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Modifier un paramètre
    @PatchMapping(value = "/{publicId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public SettingResponseDto update(
            @PathVariable UUID publicId,
            @RequestPart("data") SettingRequestDto dto,
            @RequestPart(value = "logo", required = false) MultipartFile logoFile
    ) throws IOException {

        return settingService.updateSetting(publicId, dto, logoFile);
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer une sous catégorie
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        settingService.deleteSetting(publicId);
        return ResponseEntity.noContent().build();
    }
}
