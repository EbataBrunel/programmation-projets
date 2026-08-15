package eajc.group.apv.controller;

import eajc.group.apv.dto.RoleResponseDto;
import eajc.group.apv.dto.UserResponseDto;
import eajc.group.apv.entity.Role;
import eajc.group.apv.services.RoleService;
import eajc.group.apv.services.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/users")
@PreAuthorize("hasRole('ADMIN')")
public class UserRestController {

    private final UserService userService;
    private final RoleService roleService;

    public UserRestController(UserService userService, RoleService roleService) {
        this.userService = userService;
        this.roleService = roleService;
    }

    @GetMapping("/roles")
    public ResponseEntity<List<RoleResponseDto>> getAllRoles() {
        return ResponseEntity.ok(roleService.getAllRoles());
    }

    @PostMapping("/{userId}/roles/{roleName}")
    public ResponseEntity<UserResponseDto> addRoleUser(
            @PathVariable UUID userId,
            @PathVariable String roleName
    ){
        return ResponseEntity.ok(userService.addRoleToUser(userId, roleName));
    }

    @DeleteMapping("/{userId}/roles/{roleName}")
    public ResponseEntity<UserResponseDto> removeRoleUser(
            @PathVariable UUID userId,
            @PathVariable String roleName
    ) {
        return ResponseEntity.ok(
                userService.removeRoleToUser(userId, roleName)
        );
    }

    @GetMapping
    public ResponseEntity<List<UserResponseDto>> getAll(){
        return ResponseEntity.ok(userService.findAllUsers());
    }

    @GetMapping("/{userId}")
    public ResponseEntity<UserResponseDto> getUser(@PathVariable UUID userId){
        return ResponseEntity.ok(userService.findUser(userId));
    }

    @GetMapping("/id/{userId}")
    public ResponseEntity<UserResponseDto> getUserById(@PathVariable Long userId){
        return ResponseEntity.ok(userService.findUserById(userId));
    }

    @DeleteMapping("/{userId}")
    public ResponseEntity<Void> deleteUser(@PathVariable UUID publicId){
        userService.deleteUser(publicId);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/get/{username}")
    public ResponseEntity<UserResponseDto> findUserByUsername(
            @PathVariable String username
    ){
        return ResponseEntity.ok(userService.getUserByUsername(username));
    }
}
