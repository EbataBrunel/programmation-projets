package busness.ecommerce.services;

import busness.ecommerce.dto.ProductCategoryRequestDto;
import busness.ecommerce.dto.ProductCategoryResponseDto;
import busness.ecommerce.dto.VariantProductCategoryCountResponseDto;
import busness.ecommerce.enums.Gender;

import java.util.List;

public interface ProductCategoryService {
    // CREATE
    ProductCategoryResponseDto createProductCategory(ProductCategoryRequestDto dto);

    // READ
    List<ProductCategoryResponseDto> getAllProductCategories();

    // GET
    ProductCategoryResponseDto getProductCategoryById(Long id);

    // GET
    List<ProductCategoryResponseDto> getProductCategoriesBySubCategory(Long subCategoryId);

    // UPDATE
    ProductCategoryResponseDto updateProductCategory(Long id, ProductCategoryRequestDto dto);

    // GET
    List<VariantProductCategoryCountResponseDto> countVariantsProductCategoryByGenderAndSubCategory(Gender gender, Long subCategoryId);

    // DELETE
    void deleteProductCategory(Long id);
}
