package eajc.group.apv.controller;

import eajc.group.apv.dto.GenderCountDto;
import eajc.group.apv.dto.UserProfileReasonRemovalDto;
import eajc.group.apv.dto.UserProfileRequestDto;
import eajc.group.apv.dto.UserProfileResponseDto;
import eajc.group.apv.enums.Reason;
import eajc.group.apv.services.UserProfileService;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/profiles")
public class UserProfileRestController {

    private final UserProfileService userProfileService;

    public UserProfileRestController(UserProfileService userProfileService) {
        this.userProfileService = userProfileService;
    }

    // Ajouter un client
    @PostMapping
    public ResponseEntity<UserProfileResponseDto> create(
            @RequestBody UserProfileRequestDto dto,
            @RequestParam(value = "photo", required = false) MultipartFile photoFile
    ) throws IOException  {
        return ResponseEntity.ok(userProfileService.createProfile(dto, photoFile));
    }

    // Récupérer tous les clients
    @GetMapping
    public ResponseEntity<List<UserProfileResponseDto>> getAll() {
        return ResponseEntity.ok(userProfileService.getAllProfiles());
    }

    // Récupérer un client par id
    @GetMapping("/{publicId}")
    public ResponseEntity<UserProfileResponseDto> getOne(
            @PathVariable UUID publicId
            ) {
        return ResponseEntity.ok(userProfileService.getProfileByPublicId(publicId));
    }

    // Récupérer un profile par userid
    @GetMapping("/user/{publicId}")
    public ResponseEntity<UserProfileResponseDto> getProfileUserByUser(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(userProfileService.getProfileByUser(publicId));
    }

    @GetMapping("/today")
    public ResponseEntity<List<UserProfileResponseDto>> getTodayRegistrations() {
        List<UserProfileResponseDto> profiles = userProfileService.getTodayRegistrations();
        return ResponseEntity.ok(profiles);
    }

    // Modifier un client
    @PatchMapping("/reason-removal/{publicId}")
    public ResponseEntity<UserProfileResponseDto> updateReasonRemoval(
            @PathVariable UUID publicId,
            @RequestBody UserProfileReasonRemovalDto dto
    ) {
        return ResponseEntity.ok(userProfileService.updateReasonRemoval(publicId, dto));
    }

    @GetMapping("/count-by-gender")
    public ResponseEntity<List<GenderCountDto>> countProfilesByGender() {
        return ResponseEntity.ok(
                userProfileService.countProfilesByGender()
        );
    }

    @GetMapping("/profile-by-reason-removal")
    public List<UserProfileResponseDto> getProfilesByReasonRemoval() {
        return userProfileService.getProfilesByReasonRemovalNot();
    }

    // Modifier un client
    @PatchMapping("/{publicId}")
    public ResponseEntity<UserProfileResponseDto> update(
            @PathVariable UUID publicId,
            @RequestBody UserProfileRequestDto dto
    ) {
        return ResponseEntity.ok(userProfileService.updateProfile(publicId, dto));
    }

    // Modifier un paramètre
    @PatchMapping(value = "/photo/{publicId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public UserProfileResponseDto updatePhoto(
            @PathVariable UUID publicId,
            @RequestPart(value = "photo", required = false) MultipartFile photoFile
    ) throws IOException {

        return userProfileService.updatePhotoProfile(publicId, photoFile);
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer un client
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        userProfileService.deleteProfile(publicId);
        return ResponseEntity.noContent().build();
    }

}
