package eajc.group.apv.services;

import eajc.group.apv.dto.RoleResponseDto;
import eajc.group.apv.entity.Role;

import java.util.List;

public interface RoleService {
    List<RoleResponseDto> getAllRoles();
}
