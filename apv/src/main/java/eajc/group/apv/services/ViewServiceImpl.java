package eajc.group.apv.services;

import eajc.group.apv.dto.ViewResponseDto;
import eajc.group.apv.entity.User;
import eajc.group.apv.entity.View;
import eajc.group.apv.exception.ResourceNotFoundException;
import eajc.group.apv.mapper.ViewMapper;
import eajc.group.apv.repository.UserRepository;
import eajc.group.apv.repository.ViewRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
public class ViewServiceImpl implements ViewService{

    private final ViewRepository viewRepository;
    private final UserRepository userRepository;
    private final ViewMapper viewMapper;

    public ViewServiceImpl(ViewRepository viewRepository, UserRepository userRepository, ViewMapper viewMapper) {
        this.viewRepository = viewRepository;
        this.userRepository = userRepository;
        this.viewMapper = viewMapper;
    }

    @Override
    public int createMissingViews(Long adminId) {
        User admin = userRepository.findById(adminId)
                .orElseThrow(() -> new RuntimeException("Admin introuvable"));

        List<User> usersWithoutView = viewRepository.findUsersWithoutViewForAdmin(adminId);

        List<View> views = usersWithoutView.stream()
                .map(user -> {
                    View view = new View();
                    view.setAdmin(admin);
                    view.setUser(user);
                    view.setStatus(false);
                    return view;
                })
                .toList();

        viewRepository.saveAll(views);

        return views.size();
    }

    @Override
    public List<ViewResponseDto> getViewdByAdminIdAndStatusFalse(Long adminId) {
        return viewRepository.findByAdminIdAndStatusFalse(adminId)
                .stream()
                .map(viewMapper::toDto)
                .toList();
    }

    @Override
    public ViewResponseDto getView(UUID publicId) {
        View view = viewRepository.findByPublicId(publicId)
                .orElseThrow(() -> new ResourceNotFoundException("Vue introuvable"));
        return viewMapper.toDto(view);
    }

    @Override
    @Transactional
    public int markAllViewsAsViewed(Long adminId) {
        return viewRepository.markAllViewsAsViewed(adminId);
    }

    @Override
    public int countUsersNotViewWithAdmin(Long adminId) {
        return viewRepository.countUsersNotViewWithAdmin(adminId);
    }
}
