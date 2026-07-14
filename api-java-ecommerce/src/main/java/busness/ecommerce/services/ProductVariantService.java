package busness.ecommerce.services;

import busness.ecommerce.dto.BrandVariantCountResponseDto;
import busness.ecommerce.dto.ProductVariantRequestDto;
import busness.ecommerce.dto.ProductVariantResponseDto;
import busness.ecommerce.dto.ProductVariantUpdateRequestDto;
import busness.ecommerce.enums.Gender;
import org.springframework.data.domain.Page;

import java.util.List;

public interface ProductVariantService {
    ProductVariantResponseDto create(ProductVariantRequestDto dto);
    List<ProductVariantResponseDto> getAllProductVariants();
    ProductVariantResponseDto getById(Long id);
    List<ProductVariantResponseDto> getByProduct(Long productId);
    ProductVariantResponseDto update(Long id, ProductVariantUpdateRequestDto dto);
    List<ProductVariantResponseDto> getTop3ByProductCategoryAndGender(Long productCategoryId, Gender gender);
    Page<ProductVariantResponseDto> getVariants(
            Gender gender,
            Long subCategoryId,
            int page,
            int size,
            String sortField,
            String sortDir);
    Page<ProductVariantResponseDto> getVariantsByGender(
            Gender gender,
            int page,
            int size,
            String sortField,
            String sortDir);

    Page<ProductVariantResponseDto> getVariantsByCategoryGender(
            Gender gender,
            Long categoryId,
            int page,
            int size,
            String sortField,
            String sortDir);

    Page<ProductVariantResponseDto> getVariantsByProductCategoryGender(
            Gender gender,
            Long productCategoryId,
            int page,
            int size,
            String sortField,
            String sortDir);

    Page<ProductVariantResponseDto> getVariantsByBrandsAndGender(
            Gender gender,
            List<Long> brandIds,
            int page,
            int size,
            String sortField,
            String sortDir
    );

    Page<ProductVariantResponseDto> getVariantsByBrandsAndGenderAndCategoryId(
            Gender gender,
            Long categoryId,
            List<Long> brandIds,
            int page,
            int size,
            String sortField,
            String sortDir
    );

    Page<ProductVariantResponseDto> getVariantsByBrandsAndGenderAndSubCategoryId(
            Gender gender,
            Long subCategoryId,
            List<Long> brandIds,
            int page,
            int size,
            String sortField,
            String sortDir
    );

    Page<ProductVariantResponseDto> getVariantsByBrandsAndGenderAndProductCategoryId(
            Gender gender,
            Long productCategoryId,
            List<Long> brandIds,
            int page,
            int size,
            String sortField,
            String sortDir
    );

    List<BrandVariantCountResponseDto> countVariantsByBrandForGender(Gender gender);
    List<BrandVariantCountResponseDto> countVariantsByBrandForGenderAndCategory(Gender gender, Long categoryId);
    List<BrandVariantCountResponseDto> countVariantsByBrandForGenderAndSubCategory(Gender gender, Long subCategoryId);
    List<BrandVariantCountResponseDto> countVariantsByBrandForGenderAndProductCategory(Gender gender, Long productCategoryId);
    void delete(Long id);
}
