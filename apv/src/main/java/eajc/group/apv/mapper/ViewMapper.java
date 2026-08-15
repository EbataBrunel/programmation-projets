package eajc.group.apv.mapper;

import eajc.group.apv.dto.ViewResponseDto;
import eajc.group.apv.entity.User;
import eajc.group.apv.entity.View;
import org.springframework.stereotype.Component;

@Component
public class ViewMapper {

    public View toEntity(User admin, User user){
        View view = new View();
        view.setAdmin(admin);
        view.setUser(user);

        return view;
    }

    public ViewResponseDto toDto(View view){

        ViewResponseDto dto = new ViewResponseDto();
        dto.setAdminId(view.getAdmin().getId());
        dto.setUserId(view.getUser().getId());
        dto.setUsername(view.getUser().getUsername());
        dto.setEmail(view.getUser().getEmail());
        dto.setStatus(view.getStatus());

        return  dto;
    }
}
