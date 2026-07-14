package busness.ecommerce.controller;

import busness.ecommerce.dto.BrandVariantCountResponseDto;
import busness.ecommerce.dto.ProductVariantRequestDto;
import busness.ecommerce.dto.ProductVariantResponseDto;
import busness.ecommerce.dto.ProductVariantUpdateRequestDto;
import busness.ecommerce.enums.Gender;
import busness.ecommerce.services.ProductVariantService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/product-variants")
@RequiredArgsConstructor
public class ProductVariantRestController {

    private final ProductVariantService productVariantService;

    @PostMapping
    public ProductVariantResponseDto create(
            @RequestBody ProductVariantRequestDto dto) {

        return productVariantService.create(dto);
    }

    // Récupérer toutes les catégories
    @GetMapping
    public ResponseEntity<List<ProductVariantResponseDto>> getAll() {
        return ResponseEntity.ok(productVariantService.getAllProductVariants());
    }

    // Afficher une variante
    @GetMapping("/{id}")
    public ResponseEntity<ProductVariantResponseDto> getById(@PathVariable Long id) {
        return ResponseEntity.ok(productVariantService.getById(id));
    }

    // Variantes d’un produit
    @GetMapping("/product/{productId}")
    public ResponseEntity<List<ProductVariantResponseDto>> getByProduct(
            @PathVariable Long productId
    ) {
        return ResponseEntity.ok(productVariantService.getByProduct(productId));
    }

    // Modifier
    @PatchMapping("/{id}")
    public ResponseEntity<ProductVariantResponseDto> update(
            @PathVariable Long id,
            @RequestBody ProductVariantUpdateRequestDto dto
    ) {
        return ResponseEntity.ok(productVariantService.update(id, dto));
    }

    @GetMapping("/variants")
    public ResponseEntity<Page<ProductVariantResponseDto>> getVariants(
            @RequestParam Gender gender,
            @RequestParam Long subCategoryId,
            @RequestParam int page,
            @RequestParam int size,
            @RequestParam(required = false, defaultValue = "name") String sortField,
            @RequestParam(required = false, defaultValue = "asc") String sortDir) {

        Page<ProductVariantResponseDto> variants =
                productVariantService.getVariants(gender, subCategoryId, page, size, sortField, sortDir);

        return ResponseEntity.ok(variants);
    }

    @GetMapping("/gender")
    public ResponseEntity<Page<ProductVariantResponseDto>> getVariantsByGender(
            @RequestParam Gender gender,
            @RequestParam int page,
            @RequestParam int size,
            @RequestParam(required = false, defaultValue = "name") String sortField,
            @RequestParam(required = false, defaultValue = "asc") String sortDir) {

        Page<ProductVariantResponseDto> variants =
                productVariantService.getVariantsByGender(gender, page, size, sortField, sortDir);
        return ResponseEntity.ok(variants);
    }

    @GetMapping("/category")
    public ResponseEntity<Page<ProductVariantResponseDto>> getVariantsByGenderAndCategory(
            @RequestParam Gender gender,
            @RequestParam Long categoryId,
            @RequestParam int page,
            @RequestParam int size,
            @RequestParam(required = false, defaultValue = "name") String sortField,
            @RequestParam(required = false, defaultValue = "asc") String sortDir) {

        Page<ProductVariantResponseDto> variants =
                productVariantService.getVariantsByCategoryGender(gender, categoryId, page, size, sortField, sortDir);

        return ResponseEntity.ok(variants);
    }

    @GetMapping("/category/{productCategoryId}/gender/{gender}")
    public ResponseEntity<List<ProductVariantResponseDto>> getTop6ProductVariants(
            @PathVariable Long productCategoryId,
            @PathVariable Gender gender
    ) {

        return ResponseEntity.ok(productVariantService
                .getTop3ByProductCategoryAndGender(productCategoryId, gender));

    }

    @GetMapping("/product-category")
    public ResponseEntity<Page<ProductVariantResponseDto>> getVariantsByGenderAndProductCategory(
            @RequestParam Gender gender,
            @RequestParam Long productCategoryId,
            @RequestParam int page,
            @RequestParam int size,
            @RequestParam(required = false, defaultValue = "name") String sortField,
            @RequestParam(required = false, defaultValue = "asc") String sortDir) {

        Page<ProductVariantResponseDto> variants =
                productVariantService.getVariantsByProductCategoryGender(gender, productCategoryId, page, size, sortField, sortDir);

        return ResponseEntity.ok(variants);
    }

    @GetMapping("/brand")
    public ResponseEntity<Page<ProductVariantResponseDto>> getVariantsByGenderAndBrand(
            @RequestParam Gender gender,
            @RequestParam List<Long> brandIds,
            @RequestParam int page,
            @RequestParam int size,
            @RequestParam(required = false, defaultValue = "name") String sortField,
            @RequestParam(required = false, defaultValue = "asc") String sortDir) {

        Page<ProductVariantResponseDto> variants =
                productVariantService.getVariantsByBrandsAndGender(gender, brandIds, page, size, sortField, sortDir);

        return ResponseEntity.ok(variants);
    }

    @GetMapping("/brand-category")
    public ResponseEntity<Page<ProductVariantResponseDto>> getVariantsByGenderAndCategoryAndBrand(
            @RequestParam Gender gender,
            @RequestParam Long categoryId,
            @RequestParam List<Long> brandIds,
            @RequestParam int page,
            @RequestParam int size,
            @RequestParam(required = false, defaultValue = "name") String sortField,
            @RequestParam(required = false, defaultValue = "asc") String sortDir) {

        Page<ProductVariantResponseDto> variants =
                productVariantService.getVariantsByBrandsAndGenderAndCategoryId(gender, categoryId, brandIds, page, size, sortField, sortDir);

        return ResponseEntity.ok(variants);
    }

    @GetMapping("/brand-subcategory")
    public ResponseEntity<Page<ProductVariantResponseDto>> getVariantsByGenderAndSubCategoryAndBrand(
            @RequestParam Gender gender,
            @RequestParam Long subCategoryId,
            @RequestParam List<Long> brandIds,
            @RequestParam int page,
            @RequestParam int size,
            @RequestParam(required = false, defaultValue = "name") String sortField,
            @RequestParam(required = false, defaultValue = "asc") String sortDir) {

        Page<ProductVariantResponseDto> variants =
                productVariantService.getVariantsByBrandsAndGenderAndSubCategoryId(gender, subCategoryId, brandIds, page, size, sortField, sortDir);

        return ResponseEntity.ok(variants);
    }

    @GetMapping("/brand-productcategory")
    public ResponseEntity<Page<ProductVariantResponseDto>> getVariantsByGenderAndProductCategoryAndBrand(
            @RequestParam Gender gender,
            @RequestParam Long productCategoryId,
            @RequestParam List<Long> brandIds,
            @RequestParam int page,
            @RequestParam int size,
            @RequestParam(required = false, defaultValue = "name") String sortField,
            @RequestParam(required = false, defaultValue = "asc") String sortDir) {

        Page<ProductVariantResponseDto> variants =
                productVariantService.getVariantsByBrandsAndGenderAndProductCategoryId(gender, productCategoryId, brandIds, page, size, sortField, sortDir);

        return ResponseEntity.ok(variants);
    }

    @GetMapping("/count-by-brand")
    public List<BrandVariantCountResponseDto> countVariantsByBrand(
            @RequestParam Gender gender
    ) {
        return productVariantService.countVariantsByBrandForGender(gender);
    }

    @GetMapping("/count-by-brand-for-gender-and-category")
    public List<BrandVariantCountResponseDto> countVariantsByBrandForGenderAndCategory(
            @RequestParam Gender gender,
            @RequestParam Long categoryId
    ) {
        return productVariantService.countVariantsByBrandForGenderAndCategory(gender, categoryId);
    }

    @GetMapping("/count-by-brand-for-gender-and-subcategory")
    public List<BrandVariantCountResponseDto> countVariantsByBrandForGenderAndSubCategory(
            @RequestParam Gender gender,
            @RequestParam Long subCategoryId
    ) {
        return productVariantService.countVariantsByBrandForGenderAndSubCategory(gender, subCategoryId);
    }

    @GetMapping("/count-by-brand-for-gender-and-productcategory")
    public List<BrandVariantCountResponseDto> countVariantsByBrandForGenderAndProductCategory(
            @RequestParam Gender gender,
            @RequestParam Long productCategoryId
    ) {
        return productVariantService.countVariantsByBrandForGenderAndProductCategory(gender, productCategoryId);
    }

    // Supprimer
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        productVariantService.delete(id);
        return ResponseEntity.noContent().build();
    }
}

