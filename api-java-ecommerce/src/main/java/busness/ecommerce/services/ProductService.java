package busness.ecommerce.services;

import busness.ecommerce.dto.CategoryRequestDto;
import busness.ecommerce.dto.CategoryResponseDto;
import busness.ecommerce.dto.ProductRequestDto;
import busness.ecommerce.dto.ProductResponseDto;
import busness.ecommerce.entity.Product;

import java.util.List;

public interface ProductService {
    // CREATE
    ProductResponseDto createProduct(ProductRequestDto dto);

    // READ
    List<ProductResponseDto> getAllProducts();

    // GET
    ProductResponseDto getProductById(Long id);

    // GET
    List<ProductResponseDto> getProductByPCategory(Long productCategoryId);

    // UPDATE
    ProductResponseDto updateProduct(Long id, ProductRequestDto dto);

    // DELETE
    void deleteProduct(Long id);
}
