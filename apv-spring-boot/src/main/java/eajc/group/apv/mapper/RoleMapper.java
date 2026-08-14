package eajc.group.apv.mapper;

import eajc.group.apv.dto.RoleRequestDto;
import eajc.group.apv.dto.RoleResponseDto;
import eajc.group.apv.entity.Role;
import org.springframework.stereotype.Component;

@Component
public class RoleMapper {

    public Role toEntity(RoleRequestDto dto){
        Role role = new Role();
        role.setName(role.getName());
        return role;
    }

    public RoleResponseDto toDto(Role role){
        RoleResponseDto dto = new RoleResponseDto();
        dto.setPublicId(role.getPublicId());
        dto.setName(role.getName());
        return dto;
    }
}
