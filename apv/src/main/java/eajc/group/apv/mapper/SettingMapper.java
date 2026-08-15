package eajc.group.apv.mapper;

import eajc.group.apv.dto.SettingRequestDto;
import eajc.group.apv.dto.SettingResponseDto;
import eajc.group.apv.entity.Setting;
import org.springframework.stereotype.Component;

@Component
public class SettingMapper {
    public Setting toEntity(SettingRequestDto dto, String filename){
        Setting setting = new Setting();
        setting.setNameApp(dto.getNameApp());
        setting.setNameDev(dto.getNameDev());
        setting.setVersion(dto.getVersion());
        setting.setTheme(dto.getTheme());
        setting.setBodyTheme(dto.getBodyTheme());
        setting.setTextColor(dto.getTextColor());
        setting.setCurrency(dto.getCurrency());
        setting.setAddress(dto.getAddress());
        setting.setEmail(dto.getEmail());
        setting.setPhone(dto.getPhone());
        setting.setLogo(filename);
        setting.setWidth(dto.getWidth());
        setting.setHeight(dto.getHeight());
        return setting;
    }

    public SettingResponseDto toDto(Setting dto){
        SettingResponseDto setting = new SettingResponseDto();
        setting.setPublicId(dto.getPublicId());
        setting.setNameApp(dto.getNameApp());
        setting.setNameDev(dto.getNameDev());
        setting.setVersion(dto.getVersion());
        setting.setTheme(dto.getTheme());
        setting.setBodyTheme(dto.getBodyTheme());
        setting.setTextColor(dto.getTextColor());
        setting.setCurrency(dto.getCurrency());
        setting.setAddress(dto.getAddress());
        setting.setEmail(dto.getEmail());
        setting.setPhone(dto.getPhone());
        setting.setLogo(dto.getLogo());
        setting.setWidth(dto.getWidth());
        setting.setHeight(dto.getHeight());
        return setting;
    }
}
