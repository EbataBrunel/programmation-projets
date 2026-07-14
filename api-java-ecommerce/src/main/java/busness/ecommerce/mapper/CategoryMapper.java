package busness.ecommerce.mapper;

import busness.ecommerce.dto.CategoryRequestDto;
import busness.ecommerce.dto.CategoryResponseDto;
import busness.ecommerce.dto.SubCategoryResponseDto;
import busness.ecommerce.entity.Category;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class CategoryMapper {
    public Category toEntity (CategoryRequestDto dto){
        return Category.builder()
                .name(dto.getName())
                .build();
    }


    public CategoryResponseDto toDto(Category category) {

        return CategoryResponseDto.builder()
                .id(category.getId())
                .name(category.getName())
                .subCategories(
                        category.getSubCategories() == null
                                ? List.of()
                                : category.getSubCategories()
                                    .stream()
                                    .map(sub -> SubCategoryResponseDto.builder()
                                            .id(sub.getId())
                                            .name(sub.getName())
                                            .description(sub.getDescription())
                                            .build())
                                    .toList()
                )
                .build();
    }

}
