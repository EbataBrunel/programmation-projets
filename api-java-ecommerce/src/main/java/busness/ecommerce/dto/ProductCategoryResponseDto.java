package busness.ecommerce.dto;

import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ProductCategoryResponseDto {
    private Long id;
    private String name;
    private Long subCategoryId;
    private String subCategoryName;
}
