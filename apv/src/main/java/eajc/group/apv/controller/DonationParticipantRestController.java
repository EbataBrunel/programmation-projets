package eajc.group.apv.controller;

import eajc.group.apv.dto.*;
import eajc.group.apv.services.CustomUserDetails;
import eajc.group.apv.services.DonationParticipantService;
import org.springframework.http.MediaType;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/donation-participants")
public class DonationParticipantRestController {
    private final DonationParticipantService donationParticipantService;

    public DonationParticipantRestController(DonationParticipantService donationParticipantService) {
        this.donationParticipantService = donationParticipantService;
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<DonationParticipantResponseDto> create(
            @RequestPart("data") DonationParticipantRequestDto dto,
            Authentication authentication
    ){
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("User not authenticated");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();

        return ResponseEntity.ok(donationParticipantService.createDonationParticipant(dto, user.getUser().getId()));
    }

    // Récupérer tous les participants
    @GetMapping
    public ResponseEntity<List<DonationParticipantResponseDto>> getAll() {
        return ResponseEntity.ok(donationParticipantService.getAllDonationParticipants());
    }

    // Récupérer un participant par publicId
    @GetMapping("/{publicId}")
    public ResponseEntity<DonationParticipantResponseDto> getOne(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(donationParticipantService.getDonationParticipantByPublicId(publicId));
    }

    // Récupérer tous les participants d'un don
    @GetMapping("/donation/{publicId}")
    public ResponseEntity<List<DonationParticipantResponseDto>> getParticipantsByDonation(
            @PathVariable UUID publicId
    ) {

        return ResponseEntity.ok(donationParticipantService.getParticipantsByDonation(publicId));
    }

    @GetMapping("/beneficiaries/donation-participant-count")
    public ResponseEntity<List<BeneficiaryDonationParticipantCountDto>> getCountDonationByBeneficiaryWithParticipant() {
        return ResponseEntity.ok(donationParticipantService.countDonationByBeneficiaryWithParticipant());
    }

    // Grouper le nombre de participants par don
    @GetMapping("/count-participant-by-donation/{beneficiaryPublicId}")
    public ResponseEntity<List<ParticipantsByDonationCountDto>> getCountParticipantsByDonationAndBeneficiary(
            @PathVariable UUID beneficiaryPublicId
    ) {
        return ResponseEntity.ok(donationParticipantService.countParticipantsByDonationAndBeneficiary(beneficiaryPublicId));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Modifier un participant
    @PatchMapping(value="/{publicId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<DonationParticipantResponseDto> update(
            @PathVariable UUID publicId,
            @RequestPart("data") DonationParticipantRequestDto dto,
            Authentication authentication
    ) {
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new RuntimeException("User not authenticated");
        }

        CustomUserDetails user = (CustomUserDetails) authentication.getPrincipal();

        return ResponseEntity.ok(donationParticipantService.updateDonationParticipant(publicId, dto, user.getUser().getId()));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer un participant
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        donationParticipantService.deleteDonationParticipant(publicId);
        return ResponseEntity.noContent().build();
    }
}
