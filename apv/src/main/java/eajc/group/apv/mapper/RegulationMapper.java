package eajc.group.apv.mapper;

import eajc.group.apv.dto.RegulationRequestDto;
import eajc.group.apv.dto.RegulationResponseDto;
import eajc.group.apv.entity.Regulation;
import eajc.group.apv.entity.User;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class RegulationMapper {

    public Regulation toEntity(RegulationRequestDto dto, User user){

        Regulation regulation = new Regulation();
        regulation.setDescription(dto.getDescription().trim());
        regulation.setName(dto.getName().trim());
        regulation.setUpdateAt(LocalDateTime.now());
        regulation.setUser(user);

        return regulation;
    }

    public RegulationResponseDto toDto(Regulation regulation){

        RegulationResponseDto dto = new RegulationResponseDto();

        dto.setPublicId(regulation.getPublicId());
        dto.setDescription(regulation.getDescription());
        dto.setName(regulation.getName());
        dto.setCreatedAt(regulation.getCreatedAt());
        dto.setUpdateAt(regulation.getUpdateAt());
        dto.setUserId(regulation.getUser().getId());
        dto.setUserLastName(regulation.getUser().getProfile().getLastName());
        dto.setUserFirstName(regulation.getUser().getProfile().getFirstName());

        return dto;
    }
}
