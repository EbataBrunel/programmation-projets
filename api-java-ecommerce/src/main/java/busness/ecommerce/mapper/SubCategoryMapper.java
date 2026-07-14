package busness.ecommerce.mapper;

import busness.ecommerce.dto.*;
import busness.ecommerce.entity.Category;
import busness.ecommerce.entity.SubCategory;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class SubCategoryMapper {
    public SubCategory toEntity(SubCategoryRequestDto dto, Category category){
        return SubCategory.builder()
                .name(dto.getName())
                .description(dto.getDescription())
                .category(category)
                .build();
    }

    public SubCategoryResponseDto toDto(SubCategory subCategory){
        return SubCategoryResponseDto.builder()
                .id(subCategory.getId())
                .name(subCategory.getName())
                .description(subCategory.getDescription())
                .categoryId(subCategory.getCategory().getId())
                .productCategories(subCategory.getProductCategories() == null
                        ? List.of()
                        : subCategory.getProductCategories()
                            .stream()
                            .map(pc -> ProductCategoryResponseDto.builder()
                                    .id(pc.getId())
                                    .name(pc.getName())
                                    .build())
                            .toList()
                )
                .build();
    }
}
