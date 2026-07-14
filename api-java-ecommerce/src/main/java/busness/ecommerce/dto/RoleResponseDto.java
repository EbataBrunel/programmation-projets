package busness.ecommerce.dto;

import busness.ecommerce.enums.RoleName;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class RoleResponseDto {

    private Long id;
    private RoleName name;
}

