package eajc.group.apv.services;

import eajc.group.apv.dto.ViewRequestDto;
import eajc.group.apv.dto.ViewResponseDto;

import java.util.List;
import java.util.UUID;

public interface ViewService {

    // CREATE
    int createMissingViews(Long adminId);

    // READ
    List<ViewResponseDto> getViewdByAdminIdAndStatusFalse(Long adminId);

    // GET
    public ViewResponseDto getView(UUID publicId);

    // UPDATE
    int markAllViewsAsViewed(Long adminId);

    //  GET
    int countUsersNotViewWithAdmin(Long adminId);
}
