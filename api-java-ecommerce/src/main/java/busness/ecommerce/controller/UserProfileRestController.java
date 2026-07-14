package busness.ecommerce.controller;

import busness.ecommerce.dto.SettingRequestDto;
import busness.ecommerce.dto.SettingResponseDto;
import busness.ecommerce.dto.UserProfileRequestDto;
import busness.ecommerce.dto.UserProfileResponseDto;
import busness.ecommerce.services.UserProfileService;
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
@RequestMapping(value = "/api/v1/profiles")
public class UserProfileRestController {

    private final UserProfileService clientService;

    // Ajouter un client
    @PostMapping
    public ResponseEntity<UserProfileResponseDto> create(
            @RequestBody UserProfileRequestDto dto,
            @RequestParam(value = "photo", required = false) MultipartFile photoFile
    ) throws IOException  {
        return ResponseEntity.ok(clientService.createProfile(dto, photoFile));
    }

    // Récupérer tous les clients
    @GetMapping
    public ResponseEntity<List<UserProfileResponseDto>> getAll() {
        return ResponseEntity.ok(clientService.getAllProfiles());
    }

    // Récupérer un client par id
    @GetMapping("/{id}")
    public ResponseEntity<UserProfileResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(clientService.getProfileById(id));
    }

    // Récupérer un profile par userid
    @GetMapping("/user/{id}")
    public ResponseEntity<UserProfileResponseDto> getProfileUserByUser(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(clientService.getProfileByUser(id));
    }

    // Modifier un client
    @PatchMapping("/{id}")
    public ResponseEntity<UserProfileResponseDto> update(
            @PathVariable Long id,
            @RequestBody UserProfileRequestDto dto
    ) {
        return ResponseEntity.ok(clientService.updateProfile(id, dto));
    }

    // Modifier un paramètre
    @PatchMapping(value = "/photo/{id}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public UserProfileResponseDto updatePhoto(
            @PathVariable Long id,
            @RequestPart(value = "photo", required = false) MultipartFile photoFile
    ) throws IOException {

        return clientService.updatePhotoProfile(id, photoFile);
    }

    // Supprimer un client
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        clientService.deleteProfile(id);
        return ResponseEntity.noContent().build();
    }

}
