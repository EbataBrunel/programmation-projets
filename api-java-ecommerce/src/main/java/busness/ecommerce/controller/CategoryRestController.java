package busness.ecommerce.controller;

import busness.ecommerce.dto.CategoryRequestDto;
import busness.ecommerce.dto.CategoryResponseDto;
import busness.ecommerce.services.CategoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RequiredArgsConstructor
@RestController
@RequestMapping("/api/v1/categories")
public class CategoryRestController {
    private final CategoryService categoryService;

    @PostMapping(
            consumes = MediaType.APPLICATION_JSON_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<CategoryResponseDto> create(
            @RequestBody CategoryRequestDto dto
    ){
        return ResponseEntity.ok(categoryService.createCategory(dto));
    }

    // Récupérer toutes les catégories
    @GetMapping
    public ResponseEntity<List<CategoryResponseDto>> getAll() {
        return ResponseEntity.ok(categoryService.getAllCategories());
    }

    // Récupérer une catégorie par id
    @GetMapping("/{id}")
    public ResponseEntity<CategoryResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(categoryService.getCategoryById(id));
    }

    // Modifier une catégorie
    @PutMapping("/{id}")
    public ResponseEntity<CategoryResponseDto> update(
            @PathVariable Long id,
            @RequestBody CategoryRequestDto dto
    ) {
        return ResponseEntity.ok(categoryService.updateCategory(id, dto));
    }

    // Supprimer une catégorie
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        categoryService.deleteCategory(id);
        return ResponseEntity.noContent().build();
    }
}
