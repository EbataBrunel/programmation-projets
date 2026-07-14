package busness.ecommerce.mapper;

import busness.ecommerce.dto.ProductCategoryRequestDto;
import busness.ecommerce.dto.ProductCategoryResponseDto;
import busness.ecommerce.entity.ProductCategory;
import busness.ecommerce.entity.SubCategory;
import org.springframework.stereotype.Component;

@Component
public class ProductCategoryMapper {
    public ProductCategory toEntity(ProductCategoryRequestDto dto, SubCategory subCategory){
        return ProductCategory.builder()
                .name(dto.getName())
                .subCategory(subCategory)
                .build();
    }

    public ProductCategoryResponseDto toDto(ProductCategory productCategory){
        return ProductCategoryResponseDto.builder()
                .id(productCategory.getId())
                .name(productCategory.getName())
                .subCategoryId(productCategory.getSubCategory().getId())
                .subCategoryName(productCategory.getSubCategory().getName())
                .build();
    }
}
