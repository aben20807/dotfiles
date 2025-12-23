let macvim_skip_colorscheme=1
function! s:InstallVimPlug()
    if empty(glob('~/.vim/autoload/plug.vim'))
      silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
        \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
      autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
    endif
endfunction

call s:InstallVimPlug()

call plug#begin('~/.vim/plugged')

Plug 'aben20807/vim-commenter'
let g:commenter_n_key = "<C-j>"
let g:commenter_i_key = "<C-j>"
let g:commenter_v_key = "<C-j>"

" =============================================================================
" # Color
" =============================================================================
set t_Co=256
set termguicolors
set background=dark
let base16colorspace=256
colorscheme slate
syntax on

" =============================================================================
" # Editor settings
" =============================================================================
filetype off 
filetype plugin indent on
set updatetime=300
set noesckeys " affect colortheme and remote arrow keys
set autoindent
set notimeout
set nottimeout
set encoding=utf-8
set scrolloff=2
set noshowmode
set hidden
set nowrap
set nojoinspaces
set signcolumn=no
set laststatus=2
set statusline=%F%r%h%w%=\ [%Y]\ [%04l,%04v]\ [%p%%]\ [%L]

" let new page occurred at right or below
set splitright
set splitbelow

" Proper search
set incsearch
set ignorecase
set smartcase
set gdefault
set hlsearch

" --- tab ---
set tabstop=4
set softtabstop=4
set expandtab
set shiftwidth=4

" Allow the cursor to move just past the end of the line
set virtualedit=onemore

" show detailed mode
set showmode

" let italic enable
" Ref: https://askubuntu.com/a/514524
set t_ZH=[3m
set t_ZR=[23m
" Weird char 001B[>4;m 001B[>4;2m
" Ref: https://stackoverflow.com/a/62150215/6734174
let &t_TI = ""
let &t_TE = ""
" Show those hidden characters
set listchars=nbsp:¬,extends:»,precedes:«,trail:•

" let cursor in the middle of screen when entering vim
autocmd VimEnter * :exec "normal! \zz"

" return to last edit position when opening files
autocmd BufReadPost *
            \ if line("'\"") > 0 && line("'\"") <= line('$') |
            \   exe "normal! g`\"" |
            \ endif

" let history record=1000
set history=1000
" let undo history not be clear after changing buffer
" Ref: https://stackoverflow.com/a/22676189/6734174
let vimDir = '$HOME/.config/nvim/'
let &runtimepath .= ',' . vimDir

" Keep undo history across sessions by storing it in a file
if has('persistent_undo')
    let myUndoDir = expand(vimDir . '/undodir')
    " Create dirs
    silent! call mkdir(myUndoDir, 'p')
    let &undodir = myUndoDir
    set undofile
    set undolevels=1000
    set undoreload=10000
endif
" --- backup ---
" nobackup + writebackup = backup current file, deleted afterwards (default)
" no backup
set nobackup
" write into backup file
set writebackup
" not use swap file
set noswapfile

" not auto comment when changing line
" Ref: http://vim.wikia.com/wiki/Disable_automatic_comment_insertion
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" Allow the cursor to move just past the end of the line
set virtualedit=onemore

" auto update if file changed in other way
set autoread
autocmd FileChangedShellPost *
            \ redraw | echohl WarningMsg | echo "File changed on disk. Buffer reloaded." | echohl None
function! Fresh(arg) abort
    " Ref: https://vi.stackexchange.com/a/14317
    if !bufexists("[Command Line]") | checktime | endif
endfunction
let timer = timer_start(5000,  'Fresh', {'repeat': -1})

nnoremap <expr> k (v:count == 0 ? 'gk' : 'k')
nnoremap <expr> j (v:count == 0 ? 'gj' : 'j')
inoremap <silent> <UP> <C-o>gk
inoremap <silent> <DOWN> <C-o>gj

" Fix remote terminal arrows become ABCD
nnoremap <silent> <ESC>OA <UP>
nnoremap <silent> <ESC>OB <DOWN>
nnoremap <silent> <ESC>OC <RIGHT>
nnoremap <silent> <ESC>OD <LEFT>
inoremap <silent> <ESC>OA <UP>
inoremap <silent> <ESC>OB <DOWN>
inoremap <silent> <ESC>OC <RIGHT>
inoremap <silent> <ESC>OD <LEFT>

" background vim
inoremap <C-z> <C-o><C-z>

" tab indent
vmap <TAB> >gv
vmap <S-TAB> <gv

" indent
nmap < <<
nmap > >>
vnoremap < <gv
vnoremap > >gv

" search select text by pressing // in visual mode
" Ref: http://vim.wikia.com/wiki/Search_for_visually_selected_text
vnoremap // y/\V<C-r>=escape(@",'/\')<CR><CR>
vnoremap <C-f> y/\V<C-r>=escape(@",'/\')<CR><CR>

" Not overwrite paste buffer after pasting
" Ref: https://stackoverflow.com/a/290723/6734174
function! RestoreRegister()
      let @" = s:restore_reg
        return ''
endfunction

function! s:Repl()
        let s:restore_reg = @"
            return "p@=RestoreRegister()\<CR>"
endfunction

" NB: this supports "rp that replaces the selection by the contents of @r
vnoremap <silent> <expr> p <SID>Repl()

" show line numbers, use <F2> to switch
nnoremap <F2> :set norelativenumber!<CR>:set nonumber!<CR>
:set number
:set relativenumber