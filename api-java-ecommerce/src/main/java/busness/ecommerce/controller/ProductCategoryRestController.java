package busness.ecommerce.controller;

import busness.ecommerce.dto.ProductCategoryRequestDto;
import busness.ecommerce.dto.ProductCategoryResponseDto;
import busness.ecommerce.dto.VariantProductCategoryCountResponseDto;
import busness.ecommerce.enums.Gender;
import busness.ecommerce.services.ProductCategoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping(value = "/api/v1/product-categories")
@RequiredArgsConstructor
public class ProductCategoryRestController {

    private final ProductCategoryService productCategoryService;
    // Ajouter un product-categorie
    @PostMapping
    public ResponseEntity<ProductCategoryResponseDto> create(
            @RequestBody ProductCategoryRequestDto dto
    ){
        return ResponseEntity.ok(productCategoryService.createProductCategory(dto));
    }

    // Récupérer touS les produit-categories
    @GetMapping
    public ResponseEntity<List<ProductCategoryResponseDto>> getAll() {
        return ResponseEntity.ok(productCategoryService.getAllProductCategories());
    }

    // Récupérer un product-categorie par id
    @GetMapping("/{id}")
    public ResponseEntity<ProductCategoryResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(productCategoryService.getProductCategoryById(id));
    }

    // Récupérer tous les product-categorie
    @GetMapping("/subcategory/{id}")
    public ResponseEntity<List<ProductCategoryResponseDto>> getSubcateryCategory(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(productCategoryService.getProductCategoriesBySubCategory(id));
    }

    // Regrouper les variants par product-categorie
    @GetMapping("/subcategory")
    public ResponseEntity<List<VariantProductCategoryCountResponseDto>> countVariantByGenderAndProductCategory(
            @RequestParam Gender gender,
            @RequestParam Long subCategoryId
            ) {
        return ResponseEntity.ok(productCategoryService.countVariantsProductCategoryByGenderAndSubCategory(gender, subCategoryId));
    }


    // Modifier un produit-catégorie
    @PutMapping("/{id}")
    public ResponseEntity<ProductCategoryResponseDto> update(
            @PathVariable Long id,
            @RequestBody ProductCategoryRequestDto dto
    ) {
        return ResponseEntity.ok(productCategoryService.updateProductCategory(id, dto));
    }

    // Supprimer un produit-catégorie
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        productCategoryService.deleteProductCategory(id);
        return ResponseEntity.noContent().build();
    }
}
