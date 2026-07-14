package busness.ecommerce.controller;

import busness.ecommerce.dto.BrandRequestDto;
import busness.ecommerce.dto.BrandResponseDto;
import busness.ecommerce.services.BrandService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/brands")
@RequiredArgsConstructor
public class BrandRestController {
    private final BrandService brandService;

    @PostMapping
    public BrandResponseDto create(@RequestBody BrandRequestDto request) {

        return brandService.create(request);
    }

    @GetMapping
    public List<BrandResponseDto> all() {
        return brandService.getAll();

    }

    // Récupérer une marque par id
    @GetMapping("/{id}")
    public ResponseEntity<BrandResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(brandService.getBrandById(id));
    }

    // Modifier une marque
    @PutMapping("/{id}")
    public ResponseEntity<BrandResponseDto> update(
            @PathVariable Long id,
            @RequestBody BrandRequestDto request
    ) {
        return ResponseEntity.ok(brandService.updateBrand(id, request));
    }

    // Supprimer une marque
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        brandService.deleteBrand(id);
        return ResponseEntity.noContent().build();
    }
}
