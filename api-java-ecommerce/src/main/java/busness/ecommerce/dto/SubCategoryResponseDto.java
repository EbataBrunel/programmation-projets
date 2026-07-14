package busness.ecommerce.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class SubCategoryResponseDto {
    private Long id;
    private String name;
    private String description;
    private Long categoryId;

    private List<ProductCategoryResponseDto> productCategories = new ArrayList<>();
}
