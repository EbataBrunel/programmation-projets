package eajc.group.apv.controller;

import eajc.group.apv.dto.BeneficiaryRequestDto;
import eajc.group.apv.dto.BeneficiaryResponseDto;
import eajc.group.apv.services.BeneficiaryService;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/beneficiaries")
public class BeneficiaryRestController {

    private final BeneficiaryService beneficiaryService;

    public BeneficiaryRestController(BeneficiaryService beneficiaryService) {
        this.beneficiaryService = beneficiaryService;
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<BeneficiaryResponseDto> create(
            @RequestPart("data") BeneficiaryRequestDto dto
    ){
        return ResponseEntity.ok(beneficiaryService.createBeneficiary(dto));
    }

    // Récupérer tous les bénéficiaires
    @GetMapping
    public ResponseEntity<List<BeneficiaryResponseDto>> getAll() {
        return ResponseEntity.ok(beneficiaryService.getAllBeneficiaries());
    }

    // Récupérer un bénéficiare par id
    @GetMapping("/{publicId}")
    public ResponseEntity<BeneficiaryResponseDto> getOne(
            @PathVariable UUID publicId
    ) {
        return ResponseEntity.ok(beneficiaryService.getBeneficiaryByPublicId(publicId));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Modifier un bénéficiaire
    @PatchMapping(value="/{publicId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<BeneficiaryResponseDto> update(
            @PathVariable UUID publicId,
            @RequestPart("data") BeneficiaryRequestDto dto
    ) {
        return ResponseEntity.ok(beneficiaryService.updateBeneficiary(publicId, dto));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer un bénéficiaire
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        beneficiaryService.deleteBeneficiary(publicId);
        return ResponseEntity.noContent().build();
    }
}
