package busness.ecommerce.mapper;

import busness.ecommerce.dto.SettingRequestDto;
import busness.ecommerce.dto.SettingResponseDto;
import busness.ecommerce.entity.Setting;
import org.springframework.stereotype.Component;

@Component
public class SettingMapper {
    public Setting toEntity(SettingRequestDto dto, String filename){
        return Setting.builder()
                .nameApp(dto.getNameApp())
                .nameDev(dto.getNameDev())
                .version(dto.getVersion())
                .theme(dto.getTheme())
                .textColor(dto.getTextColor())
                .currency(dto.getCurrency())
                .address(dto.getAddress())
                .email(dto.getEmail())
                .phone(dto.getPhone())
                .logo(filename)
                .width(dto.getWidth())
                .height(dto.getHeight())
                .build();
    }

    public SettingResponseDto toDto(Setting setting){
        return SettingResponseDto.builder()
                .id(setting.getId())
                .nameApp(setting.getNameApp())
                .nameDev(setting.getNameDev())
                .version(setting.getVersion())
                .theme(setting.getTheme())
                .textColor(setting.getTextColor())
                .currency(setting.getCurrency())
                .address(setting.getAddress())
                .email(setting.getEmail())
                .phone(setting.getPhone())
                .logo(setting.getLogo())
                .width(setting.getWidth())
                .height(setting.getHeight())
                .build();
    }
}
