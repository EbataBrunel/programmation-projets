package busness.ecommerce.controller;

import busness.ecommerce.dto.ProductRequestDto;
import busness.ecommerce.dto.ProductResponseDto;
import busness.ecommerce.services.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RequiredArgsConstructor
@RestController
@RequestMapping(value = "/api/v1/products")
public class ProductRestController {
    private final ProductService productService;
    // Ajouter un produit
    @PostMapping
    public ResponseEntity<ProductResponseDto> create(
            @RequestBody ProductRequestDto dto
    ){
        return ResponseEntity.ok(productService.createProduct(dto));
    }

    // Récupérer tous les produits
    @GetMapping
    public ResponseEntity<List<ProductResponseDto>> getAll() {
        return ResponseEntity.ok(productService.getAllProducts());
    }

    // Récupérer un produit par id
    @GetMapping("/{id}")
    public ResponseEntity<ProductResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(productService.getProductById(id));
    }

    // Récupérer un produit par subcategory
    @GetMapping("/product-category/{id}")
    public ResponseEntity<List<ProductResponseDto>> getProductByPCategory(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(productService.getProductByPCategory(id));
    }

    // Modifier un produit
    @PreAuthorize("hasRole('ADMIN')")
    @PatchMapping("/{id}")
    public ResponseEntity<ProductResponseDto> update(
            @PathVariable Long id,
            @RequestBody ProductRequestDto dto
    ) {
        return ResponseEntity.ok(productService.updateProduct(id, dto));
    }

    // Supprimer un produit
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        productService.deleteProduct(id);
        return ResponseEntity.noContent().build();
    }
}
