package busness.ecommerce.dto;

import lombok.*;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BrandResponseDto {
    private Long id;
    private String name;
    private List<ProductResponseDto> products = new ArrayList<>();
}
