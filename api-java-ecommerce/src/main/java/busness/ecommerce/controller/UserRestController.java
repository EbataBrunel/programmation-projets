package busness.ecommerce.controller;

import busness.ecommerce.dto.UserResponseDto;
import busness.ecommerce.entity.User;
import busness.ecommerce.enums.RoleName;
import busness.ecommerce.services.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RequiredArgsConstructor
@RestController
@RequestMapping(value = "/api/v1/users")
@PreAuthorize("hasRole('ADMIN')")
public class UserRestController {

    private final UserService userService;

    @PostMapping("/{userId}/roles/{roleName}")
    public ResponseEntity<UserResponseDto> addRoleUser(
            @PathVariable Long userId,
            @PathVariable RoleName roleName
    ){
        return ResponseEntity.ok(userService.addRoleToUser(userId, roleName));
    }

    @GetMapping
    public ResponseEntity<List<UserResponseDto>> getAll(){
        return ResponseEntity.ok(userService.findAllUsers());
    }

    @GetMapping("/{userId}")
    public ResponseEntity<UserResponseDto> getUser(@PathVariable Long userId){
        return ResponseEntity.ok(userService.findUser(userId));
    }

    @DeleteMapping("/{userId}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long userId){
        userService.deleteUser(userId);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/get/{username}")
    public ResponseEntity<UserResponseDto> findUserByUsername(
            @PathVariable String username
    ){
        return ResponseEntity.ok(userService.getUserByUsername(username));
    }
}
