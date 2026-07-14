package busness.ecommerce.controller;

import busness.ecommerce.dto.*;
import busness.ecommerce.services.SettingService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RequiredArgsConstructor
@RestController
@RequestMapping(value="/api/v1/settings")
public class SettingRestController {

    private final SettingService settingService;
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

    // Récupérer un paramètre par id
    @GetMapping("/{id}")
    public ResponseEntity<SettingResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(settingService.getSettingById(id));
    }

    // Récupérer le dernier paramètre
    @GetMapping("/latest")
    public ResponseEntity<SettingResponseDto> getLast() {
        return ResponseEntity.ok(settingService.getLastSetting());
    }

    // Modifier un paramètre
    @PatchMapping(value = "/{id}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public SettingResponseDto update(
            @PathVariable Long id,
            @RequestPart("data") SettingRequestDto dto,
            @RequestPart(value = "logo", required = false) MultipartFile logoFile
    ) throws IOException {

        return settingService.updateSetting(id, dto, logoFile);
    }

    // Supprimer une sous catégorie
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        settingService.deleteSetting(id);
        return ResponseEntity.noContent().build();
    }
}
