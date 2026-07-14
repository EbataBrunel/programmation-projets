package busness.ecommerce.mapper;

import busness.ecommerce.dto.RoleResponseDto;
import busness.ecommerce.entity.Role;
import org.springframework.stereotype.Component;

@Component
public class RoleMapper {
    public RoleResponseDto toDto(Role role){
        return new RoleResponseDto(
                role.getId(),
                role.getName()
        );
    }
}
