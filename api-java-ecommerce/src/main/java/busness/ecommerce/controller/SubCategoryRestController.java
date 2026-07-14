package busness.ecommerce.controller;

import busness.ecommerce.dto.SubCategoryRequestDto;
import busness.ecommerce.dto.SubCategoryResponseDto;
import busness.ecommerce.services.SubCategoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping(value = "/api/v1/subcategories")
@RequiredArgsConstructor
public class SubCategoryRestController {

    private final SubCategoryService subCategoryService;

    // Ajouter une sous catégorie
    @PostMapping
    public ResponseEntity<SubCategoryResponseDto> create(
            @RequestBody SubCategoryRequestDto dto
    ){
       return ResponseEntity.ok(subCategoryService.createSubCategory(dto));
    }

    // Récupérer toutes les sous catégories
    @GetMapping
    public ResponseEntity<List<SubCategoryResponseDto>> getAll() {
        return ResponseEntity.ok(subCategoryService.getAllSubCategories());
    }

    // Récupérer une sous catégorie par id
    @GetMapping("/{id}")
    public ResponseEntity<SubCategoryResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(subCategoryService.getSubCategoryById(id));
    }

    // Récupérer toutes les sous catégories d'une catégorie
    @GetMapping("/category/{id}")
    public ResponseEntity<List<SubCategoryResponseDto>> getSubcateryCategory(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(subCategoryService.getSubCategoriesByCategory(id));
    }

    // Modifier une sous catégorie
    @PutMapping("/{id}")
    public ResponseEntity<SubCategoryResponseDto> update(
            @PathVariable Long id,
            @RequestBody SubCategoryRequestDto dto
    ) {
        return ResponseEntity.ok(subCategoryService.updateSubCategory(id, dto));
    }

    // Supprimer une sous catégorie
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        subCategoryService.deleteSubCategory(id);
        return ResponseEntity.noContent().build();
    }
}
