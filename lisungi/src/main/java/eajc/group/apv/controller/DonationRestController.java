package eajc.group.apv.controller;


import eajc.group.apv.dto.*;
import eajc.group.apv.services.CaptchaService;
import eajc.group.apv.services.DonationService;
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
@RequestMapping("/api/v1/donations")
public class DonationRestController {

    private final DonationService donationService;
    private final CaptchaService captchaService;

    public DonationRestController(DonationService donationService, CaptchaService captchaService) {
        this.donationService = donationService;
        this.captchaService = captchaService;
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<DonationResponseDto> create(
            @RequestPart("data") DonationRequestDto dto,
            @RequestParam(value = "photo", required = false) MultipartFile photoFile
    ) throws IOException {

        return ResponseEntity.ok(donationService.createDonation(dto, photoFile));
    }

    // Récupérer tous les dons
    @GetMapping
    public ResponseEntity<List<DonationResponseDto>> getAll() {
        return ResponseEntity.ok(donationService.getAllDonations());
    }

    // Récupérer un don par publicId
    @GetMapping("/{publicId}")
    public ResponseEntity<DonationResponseDto> getOne(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(donationService.getDonationByPublicId(publicId));
    }

    // Récupérer un don par id
    @GetMapping("/id/{id}")
    public ResponseEntity<DonationResponseDto> getDonationById(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(donationService.getDonationById(id));
    }

    // Regrouper le nombre de don par bénéficiaire
    @GetMapping("/count/donation")
    public ResponseEntity<List<BeneficiaryCountDto>> getCountDonationsByBeneficiary() {
        return ResponseEntity.ok(donationService.countDonationsByBeneficiary());
    }

    // Récuperer un don par bénéfiaire
    @GetMapping("/donations/{beneficiaryId}")
    public ResponseEntity<List<DonationResponseDto>> findDonationsByBeneficiaryId(
            @PathVariable Long beneficiaryId
    ) {

        return ResponseEntity.ok(donationService.findByBeneficiaryId(beneficiaryId));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Modifier la visibilité d'un don
    @PatchMapping("/update-visibility/{publicId}")
    public ResponseEntity<DonationResponseDto> updateVisibilite(
            @PathVariable UUID publicId
    ) {

        return ResponseEntity.ok(donationService.updateVisibilityDonation(publicId));
    }

    @PreAuthorize("hasRole('SUPADMIN')")
    // Modifier le statut don
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

        return ResponseEntity.ok(donationService.updateClosureStatusDonation(publicId));
    }

    @GetMapping("/statistics/by-year")
    public ResponseEntity<List<DonationCountByYearDto>> countDonationsByYear() {
        return ResponseEntity.ok(
                donationService.countDonationsByYear()
        );
    }

    @GetMapping("/month")
    public ResponseEntity<List<DonationResponseDto>> getDonationsByMonth(
            @RequestParam int year,
            @RequestParam int month
    ) {
        return ResponseEntity.ok(
                donationService.getDonationsByMonth(year, month)
        );
    }

    @GetMapping("/year")
    public ResponseEntity<List<DonationResponseDto>> getDonationsByYear(
            @RequestParam int year
    ) {
        return ResponseEntity.ok(
                donationService.getDonationsByYear(year)
        );
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Modifier un don
    @PatchMapping(value="/{publicId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<DonationResponseDto> update(
            @PathVariable UUID publicId,
            @RequestPart("data") DonationRequestDto dto,
            @RequestParam(value = "photo", required = false) MultipartFile photoFile
    ) throws IOException {
        return ResponseEntity.ok(donationService.updateDonation(publicId, dto, photoFile));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer un don
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        donationService.deleteDonation(publicId);
        return ResponseEntity.noContent().build();
    }

}
